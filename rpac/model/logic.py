# -*- coding: utf-8 -*-
import os
import traceback

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.sql.expression import and_, desc
from sqlalchemy.orm import synonym
from sqlalchemy.types import Integer, Text, DateTime

from tg import config

from rpac.model import DeclarativeBase, qry
from interface import SysMixin, nextVal
from auth import User


__all__ = [
           'STATUS_NEW', 'STATUS_UNDER_DEV', 'STATUS_APPROVE', 'STATUS_CANCEL', 'STATUS_DISCONTINUE',
           'FILE_CHECK_IN', 'FILE_CHECK_OUT',
           'Item', 'FileObject',
            ]

STATUS_NEW = 0
STATUS_UNDER_DEV = 1
STATUS_APPROVE = 2
STATUS_CANCEL = -1
STATUS_DISCONTINUE = 9
FILE_CHECK_IN = 0
FILE_CHECK_OUT = 1





class Item( DeclarativeBase, SysMixin ):

    __tablename__ = 'logic_item'

    id = Column( Integer, primary_key = True )
    systemNo = Column( "system_no", Text )
    jobNo = Column( "job_no", Text )
    desc = Column( "desc", Text )
    files = Column( "files", Text )
    approveFileIDs = Column( "approve_files_ids", Text )
    approveFilesZipID = Column( "approve_files_zip_id", Integer )

    approveTime = Column( 'approve_time', DateTime )
    approveById = Column( 'approve_by_id', Integer )
    status = Column( "status", Integer, default = STATUS_NEW )

    def __init__( self, *args, **kwargs ):
        super( self.__class__, self ).__init__( *args, **kwargs )
        seq = nextVal( 'logic_item_seq' )
        self.systemNo = 'FD%.9d' % seq


    @property
    def approveBy( self ):  return qry( User ).get( self.approveById )


    def getFiles( self ):
        if not self.files : return []
        _ids = filter( bool, self.files.split( "|" ) )
        if not _ids : return []
        return qry( FileObject ).filter( and_( FileObject.active == 0 , FileObject.id.in_( _ids ) ) ).order_by( desc( FileObject.updateTime ) )

    def getApproveFiles( self ):
        if not self.approveFileIDs : return []
        _ids = filter( bool, self.approveFileIDs.split( "|" ) )
        if not _ids or self.status != STATUS_APPROVE : return []
        return qry( FileObject ).filter( and_( FileObject.active == 0 , FileObject.id.in_( _ids ) ) ).order_by( desc( FileObject.updateTime ) )

    def showStatus( self ):
        return {
                STATUS_NEW : 'New',
                STATUS_UNDER_DEV :'Under Development',
                STATUS_APPROVE : 'Approved',
                STATUS_CANCEL :'Cancelled',
                STATUS_DISCONTINUE : 'Discontinued',
                }.get( self.status, '' )




class FileObject( DeclarativeBase, SysMixin ):
    __tablename__ = 'logic_file_object'

    id = Column( Integer, primary_key = True )
    fileName = Column( "file_name", Text )
    _file_path = Column( "file_path", Text, nullable = False )
    referto = Column( Text )
    share = Column( Text )    #'Y' to be share
    status = Column( Integer, default = FILE_CHECK_IN )
    checkoutById = Column( 'checkout_by_id', Integer )

    @property
    def checkoutBy( self ):
        return qry( User ).get( self.checkoutById )

    def _get_file_path( self ):
        return os.path.join( config.get( "file_dir" ), self._file_path )

    def _set_file_path( self, value ):
        self._file_path = value

    filePath = synonym( '_file_path', descriptor = property( _get_file_path, _set_file_path ) )
